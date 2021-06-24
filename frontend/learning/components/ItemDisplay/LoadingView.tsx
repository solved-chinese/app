import React from "react";
import ContentLoader from "react-content-loader";

const MyLoader = (): JSX.Element => (
  <ContentLoader
    speed={2}
    width={700}
    height={200}
    viewBox="0 0 700 200"
    backgroundColor="#f3f3f3"
    foregroundColor="#ecebeb"
  >
    <rect x="300" y="40" rx="3" ry="3" width="88" height="6" />
    <rect x="300" y="55" rx="3" ry="3" width="52" height="6" />
    <rect x="100" y="160" rx="3" ry="3" width="410" height="6" />
    <rect x="100" y="120" rx="3" ry="3" width="380" height="6" />
    <rect x="100" y="140" rx="3" ry="3" width="178" height="6" />
    <circle cx="230" cy="55" r="30" />
    <rect x="300" y="70" rx="3" ry="3" width="70" height="6" />
  </ContentLoader>
);

export default MyLoader;
