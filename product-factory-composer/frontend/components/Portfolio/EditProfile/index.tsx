import React, {useEffect, useState} from "react";
import {Category, EditProfileProps, ProfileType, Skill, SkillExpertise, Website} from "../interfaces";
import {Avatar, Button, Col, Input, message, Row, Select, Typography, Upload} from "antd";
import {UploadFile} from "antd/es/upload/interface";
import {useRouter} from "next/router";
import ImgCrop from "antd-img-crop";
import 'antd/es/modal/style';
import 'antd/es/slider/style';
import {useMutation, useQuery} from "@apollo/react-hooks";
import {UPDATE_PERSON, SAVE_AVATAR, DELETE_AVATAR} from "../../../graphql/mutations";
import {getProp} from "../../../utilities/filters";
import {apiDomain} from "../../../utilities/constants";
import SkillsArea from "./SkillComponents/SkillArea";
import ExpertiseArea from "./SkillComponents/ExpertiseArea";
import {DeleteOutlined, PlusOutlined, UserOutlined} from "@ant-design/icons";
import {GET_CATEGORIES_LIST} from "../../../graphql/queries";
import {findExpertise} from "../helpers";

const {Option} = Select;

const EditProfile = ({profile, setProfile}: EditProfileProps) => {
  const [firstName, setFirstName] = useState<string>(profile.firstName.split(' ')[0]);
  const [lastName, setLastName] = useState<string>(profile.firstName.split(' ')[1]);
  const [bio, setBio] = useState<string>(profile.bio);
  const [skills, setSkills] = useState<Skill[]>(profile.skills);
  const [websites, setWebsites] = useState<Website[]>(profile.websites);
  const [websiteTypes, setWebsiteTypes] = useState<string[]>(profile.websiteTypes);
  const [avatarId, setAvatarId] = useState<number>(-1);
  const [avatarUrl, setAvatarUrl] = useState<string>(profile.avatar);
  const [uploadStatus, setUploadStatus] = useState<boolean>(false);
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [allCategories, setAllCategories] = useState<Category[]>([]);
  const [skillExpertise, setSkillExpertise] = useState<SkillExpertise[]>([]);
  const [expertiseList, setExpertiseList] = useState<string[]>([]);

  const {data: categories} = useQuery(GET_CATEGORIES_LIST);
  const [deleteAvatar] = useMutation(DELETE_AVATAR, {
    onCompleted(data) {
      const status = getProp(data, 'deleteAvatar.status', false);
      const messageText = getProp(data, 'deleteAvatar.message', '');

      if (status) {
        message.success('Avatar successfully deleted').then();

        setProfile((prevState: ProfileType) => {
          return {...prevState, avatar: ''}
        });
        setAvatarUrl('');
        setAvatarId(-1);
      } else {
        message.error(messageText).then();
      }
    },
    onError() {
      message.error('Error with person profile updating').then();
    }
  });

  useEffect(() => {
    if (categories?.taskCategoryListing) {
      setAllCategories(JSON.parse(categories.taskCategoryListing));
    }
  }, [categories]);

  const router = useRouter();
  let { personSlug } = router.query;

  const onDeleteAvatarClick = () => {
    deleteAvatar({
      variables: {
        personSlug,
      }
    }).then();
  }

  useEffect(() => {
    if (allCategories) {
      setFirstName(profile.firstName.split(' ')[0]);
      setLastName(profile.firstName.split(' ')[1]);
      setBio(profile.bio);
      setWebsites(profile.websites);
      setWebsiteTypes(profile.websiteTypes);
      setAvatarUrl(profile.avatar);
      setFileList([]);
      setSkills(profile.skills);
      const currentSkillExpertise: SkillExpertise[] = [];
      profile.skills.map(skill => {
        currentSkillExpertise.push({
          skill: skill.category,
          expertise: findExpertise(skill.category, allCategories)
        });
      });
      setSkillExpertise(currentSkillExpertise);
      setExpertiseList(profile.skills.map(skill => skill.expertise ? skill.expertise : skill.category));
    }
  }, [profile, allCategories]);

  const [updateProfile] = useMutation(UPDATE_PERSON, {
    onCompleted(data) {
      const status = getProp(data, 'updatePerson.status', false);
      const messageText = getProp(data, 'updatePerson.message', '');

      if (status) {
        message.success("Person profile successfully updated", 10).then();
        router.back();
      } else {
        message.error(messageText).then();
      }
    },
    onError() {
      message.error('Error with person profile updating').then();
    }
  });

  const [saveAvatar] = useMutation(SAVE_AVATAR, {
    onCompleted(data) {
      const status = getProp(data, 'saveAvatar.status', false);
      const messageText = getProp(data, 'saveAvatar.message', '');

      if (status) {
        message.success("Avatar successfully uploaded", 10).then();
        setAvatarUrl(apiDomain + data.saveAvatar.avatarUrl);
        setAvatarId(data.saveAvatar.avatarId);
      } else {
        message.error(messageText).then();
      }
    },
    onError() {
      message.error('Upload file failed').then();
    }
  });

  const checkFileList = (fileList: any) => {
    const thumbUrl = fileList[0].thumbUrl;
    const url = fileList[0].url;
    return thumbUrl ? thumbUrl : url;
  }

  const onUploadChange = ({fileList}: any) => {
    if (fileList.length > 0 && !uploadStatus) {
      setUploadStatus(true);
      setTimeout(() => saveAvatar({variables: {avatar: checkFileList(fileList)}}).then(), 1000);
      setTimeout(() => setUploadStatus(false), 3000);
    }
    setFileList(fileList);
  }

  const save = () => {
    let newSkills: any[] = [];
    for (let skill of skills) {
      newSkills.push({category: skill.category, expertise: skill.expertise});
    }
    let newWebsites: any[] = [];
    for (let website of websites) {
      newWebsites.push({type: website.type, website: website.website})
    }
    const variables = {
      firstName,
      lastName,
      bio,
      skills: newSkills,
      websites: newWebsites,
      avatar: avatarId
    }
    updateProfile({variables: variables}).then();
  }

  const onImagePreview = async (file: any) => {
    let src = file.url;
    if (!src) {
      src = await new Promise(resolve => {
        const reader = new FileReader();
        reader.readAsDataURL(file.originFileObj);
        reader.onload = () => resolve(reader.result);
      });
    }
    const image = new Image();
    image.src = src;
    const imgWindow = window.open(src);
    imgWindow && imgWindow.document.write(image.outerHTML);
  };

  const changeWebsitesCount = () => {
    setWebsites((prevState => [...prevState, {website: '', type: 0}]))
  }

  const changeWebsite = (value: string, index: number) => {
    setWebsites(prevState => {
      const newObj = prevState[index];
      newObj.website = value;
      return [...prevState.slice(0, index), newObj, ...prevState.slice(index + 1)];
    });
  }

  const changeWebsiteType = (value: string, index: number) => {
    setWebsites(prevState => {
      const newObj = prevState[index];
      newObj.type = websiteTypes.indexOf(value);
      return [...prevState.slice(0, index), newObj, ...prevState.slice(index + 1)];
    });
  }

  return (
    <Row gutter={[52, 0]} justify={"center"} style={{margin: "5% auto"}}>
      <Col>
        {
          fileList.length > 1 || !profile.avatar ? <ImgCrop shape={'round'} modalOk={"Crop"} rotate>
            <Upload className="avatar-upload"
                    onChange={onUploadChange}
                    fileList={fileList}
                    showUploadList={true}
                    listType={"picture-card"}
                    onPreview={onImagePreview}
            >
              { fileList.length < 1 && '+ Upload' }
            </Upload>
          </ImgCrop> : <span style={{ position: 'relative' }}>
            <Avatar size={80} icon={<UserOutlined/>} src={apiDomain + profile.avatar}/>
            <DeleteOutlined onClick={onDeleteAvatarClick} style={{ position: 'absolute', top: -25, right: -5 }} />
          </span>
        }
      </Col>
      <Col>
        <Row gutter={[48, 0]}>
          <Col>
            <Row justify={"start"} style={{marginBottom: 20}}>
              <Typography.Text strong>First Name</Typography.Text>
            </Row>
            <Row style={{marginBottom: 20}}>
              <Input placeholder={"First Name"} value={firstName}
                     onChange={(e) => setFirstName(e.target.value)}/>
            </Row>
          </Col>
          <Col>
            <Row justify={"start"} style={{marginBottom: 20}}>
              <Typography.Text strong>Last Name</Typography.Text>
            </Row>
            <Row style={{marginBottom: 20}}>
              <Input placeholder={"Last Name"} value={lastName}
                     onChange={(e) => setLastName(e.target.value)}/>
            </Row>
          </Col>
        </Row>
        <Row>
          <Col>
            <Row justify={"start"} style={{marginBottom: 20}}>
              <Typography.Text strong>Bio</Typography.Text>
            </Row>
            <Row style={{marginBottom: 20}}>
              <Input.TextArea autoSize={true} style={{width: 460}} value={bio} placeholder={"Bio"}
                              onChange={(e) => setBio(e.target.value)}/>
            </Row>
          </Col>
        </Row>
        <Row>
          <Col>
            <Row justify={"start"} style={{marginBottom: 20}}>
              <Typography.Text strong>Skills</Typography.Text>
            </Row>
            <Row style={{marginBottom: 20}}>
              <SkillsArea setSkills={setSkills}
                          skillExpertise={skillExpertise}
                          setExpertiseList={setExpertiseList} setSkillExpertise={setSkillExpertise}
                          allCategories={allCategories}/>
            </Row>
          </Col>
        </Row>
        <Row>
          <Col>
            <Row justify={"start"} style={{marginBottom: 20}}>
              <Typography.Text strong>Expertise</Typography.Text>
            </Row>
            <Row style={{marginBottom: 20}}>
              <ExpertiseArea setSkills={setSkills} setSkillExpertise={setSkillExpertise}
                             allCategories={allCategories}
                             skillExpertise={skillExpertise} expertiseList={expertiseList}
                             setExpertiseList={setExpertiseList}/>
            </Row>
          </Col>
        </Row>
        <Row>
          <Col>
            <Row justify={"start"} style={{marginBottom: 20}}>
              <Col>
                <Row>
                  <Typography.Text strong>Websites</Typography.Text>
                </Row>
                <Row>
                  <Typography.Text style={{marginTop: 5, color: "#8C8C8C", fontSize: 8.5}}>Add the URL
                    links here:</Typography.Text>
                </Row>
              </Col>
            </Row>
            {websites.length > 0 && websites.map((website, index) => (
              <Row key={index} style={{marginBottom: 20}}>
                <Col>
                  <Row gutter={[15, 0]}>
                    <Col>
                      <Input addonBefore={"https://"} placeholder={"Website"}
                             value={website.website} style={{width: 350}}
                             onChange={(e) => changeWebsite(e.target.value, index)}/>
                    </Col>
                    <Col>
                      <Select onChange={(e) => changeWebsiteType(e, index)}
                              value={websiteTypes[website.type]}>
                        {websiteTypes.map(websiteType => (
                          <Option value={websiteType}>{websiteType}</Option>
                        ))}
                      </Select>
                    </Col>
                  </Row>
                </Col>
              </Row>
            ))}
            <Row align={"middle"}>
              <Button size={"small"}
                      style={{fontSize: 11, border: "none", padding: 0, color: "#1890FF"}}
                      onClick={changeWebsitesCount}><PlusOutlined style={{marginRight: 3}}/> Add
                website</Button>
            </Row>
          </Col>
        </Row>
        <Row justify={"start"} style={{marginBottom: 20}}>
          <Button type={"primary"} style={{width: 108, height: 33, marginRight: 20}}
                  onClick={save}>Save</Button>
          <Button size={"large"} style={{width: 108, height: 33}}
                  onClick={() => router.back()}>Cancel</Button>
        </Row>
      </Col>
    </Row>
  )
    ;
}

export default EditProfile;
