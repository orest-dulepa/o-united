ALTER TABLE public.users_user OWNER TO ou;

ALTER TABLE public.black_listed_usernames OWNER TO ou;

ALTER TABLE public.capability OWNER TO ou;

ALTER TABLE public.comments_capabilitycomment OWNER TO ou;

ALTER TABLE public.comments_ideacomment OWNER TO ou;

ALTER TABLE public.comments_taskcomment OWNER TO ou;

ALTER TABLE public.comments_ideacomment OWNER TO ou;

ALTER TABLE public.commercial_organisation OWNER TO ou;

ALTER TABLE public.commercial_productowner OWNER TO ou;

ALTER TABLE public.django_session OWNER TO ou;

ALTER TABLE public.ideas_bugs_idea OWNER TO ou;

ALTER TABLE public.ideas_bugs_ideavote OWNER TO ou;

ALTER TABLE public.license_contributor_agreement OWNER TO ou;

ALTER TABLE public.license_contributor_agreement_acceptance OWNER TO ou;

ALTER TABLE public.license_contributorguide OWNER TO ou;

ALTER TABLE public.license_license OWNER TO ou;

ALTER TABLE public.matching_taskclaim OWNER TO ou;

ALTER TABLE public.notifications_notification OWNER TO ou;

ALTER TABLE public.pages_page OWNER TO ou;

ALTER TABLE public.talent_person OWNER TO ou;

ALTER TABLE public.talent_personprofile OWNER TO ou;

ALTER TABLE public.talent_productperson OWNER TO ou;

ALTER TABLE public.talent_review OWNER TO ou;

ALTER TABLE public.talent_socialaccount OWNER TO ou;

ALTER TABLE public.work_attachment OWNER TO ou;

ALTER TABLE public.work_createproductrequest OWNER TO ou;

ALTER TABLE public.work_initiative OWNER TO ou;

ALTER TABLE public.work_product OWNER TO ou;

ALTER TABLE public.work_product_attachment OWNER TO ou;

ALTER TABLE public.work_producttask OWNER TO ou;

ALTER TABLE public.work_tag OWNER TO ou;

ALTER TABLE public.work_task OWNER TO ou;

ALTER TABLE public.work_task_attachment OWNER TO ou;

ALTER TABLE public.work_task_depend OWNER TO ou;

ALTER TABLE public.work_task_tag OWNER TO ou;

ALTER TABLE public.work_tasklisting OWNER TO ou;

INSERT INTO public.black_listed_usernames(username)
VALUES ('account'),
       ('admin'),
       ('api'),
       ('blog'),
       ('cache'),
       ('changelog'),
       ('enterprise'),
       ('gist'),
       ('graphql'),
       ('help'),
       ('jobs'),
       ('lists'),
       ('login'),
       ('logout'),
       ('mine'),
       ('news'),
       ('plans'),
       ('popular'),
       ('projects'),
       ('products'),
       ('about'),
       ('pages'),
       ('privacy'),
       ('privacy-policy'),
       ('terms-of-use'),
       ('security'),
       ('shop'),
       ('translations'),
       ('signup'),
       ('status'),
       ('styleguide'),
       ('tour'),
       ('wiki'),
       ('stories'),
       ('organizations'),
       ('codereview'),
       ('better'),
       ('compare'),
       ('hosting'),
       ('site'),
       ('content'),
       ('cms'),
       ('style'),
       ('setup'),
       ('console'),
       ('user');