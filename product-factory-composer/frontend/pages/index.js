import Dashboard from "../components/Dashboard";
import Header from "../components/Header";
import withApollo from "../lib/apolloClient";
import ContainerFlex from "../components/ContainerFlex";
import { Layout } from "antd";
import Footer from "../components/Footer";
import Head from "next/head";

function Home() {
  return (
    <ContainerFlex>
      <Head>
        <title>OU</title>
        <meta
          name="description"
          content="OU - the place where communities - comprising contributors of all kinds - come together to create and contribute to Open Products."
        />
        <link
            rel="preload"
            href="/fonts/Roboto/Roboto-Black.ttf"
            as="font"
            crossOrigin=""
        />
      </Head>
      <Layout style={{ minHeight: "100vh" }}>
        <Header />
        <Dashboard />
        <Footer />
      </Layout>
    </ContainerFlex>
  );
}

export default withApollo({ ssr: true })(Home);
