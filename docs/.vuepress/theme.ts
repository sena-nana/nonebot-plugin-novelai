import { hopeTheme } from "vuepress-theme-hope";
import navbar from "./navbar";

export default hopeTheme({
  hostname: "https://sena-nana.github.io/MutsukiDocs",
  author: {
    name: "星奈 Sena",
    url: "https://github.com/sena-nana",
  },

  //pure:true,
  themeColor:{
      blue: "#2196f3",
      red: "#f26d6d",
      green: "#3eaf7c",
      orange: "#fb9b5f",
  },
  backToTop:true,
  iconAssets: "iconfont",
  logo: "",
  repo: "sena-nana/MutsukiBot",
  lastUpdated:true,
  navbar: navbar,
  sidebar: {
    "/main/":"structure",
    "/update/":"structure",
  },
  footer: "后面没有了哦~",
  displayFooter: true,
  copyright:"MIT Licensed / CC-BY-NC-SA | Copyright © 2022-present 星奈 Sena",
  pageInfo: ["Author", "ReadingTime","Word"],
  encrypt: {
    config: {
      "/guide/encrypt.html": ["1234"],
    },
  },
  plugins: {
    blog: {
      autoExcerpt: true,
    },
    git:{
      updatedTime: true,
      contributors:true,
      createdTime:false,
    },
    photoSwipe:{},
    pwa:{
      showInstall: true,
    },
    sitemap:{},
    mdEnhance: {
      gfm:true,
      container:true,
      tabs:true,
      codetabs:true,
      align:true,
      tasklist:true,
      flowchart:true,
      stylize:[],
      presentation: false,
    },
  },
});
