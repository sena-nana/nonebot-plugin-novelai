import { hopeTheme } from "vuepress-theme-hope";
import navbar from "./navbar";

export default hopeTheme({
  hostname: "https://sena-nana.github.io/MutsukiDocs",
  author: {
    name: "星奈奈奈 Senanana",
    url: "https://github.com/sena-nana",
  },

  //pure:true,
  themeColor: {
    blue: "#2196f3",
    red: "#f26d6d",
    green: "#3eaf7c",
    orange: "#fb9b5f",
  },
  backToTop: true,
  iconAssets: "iconfont",
  logo: "",
  repo: "sena-nana/MutsukiBot",
  lastUpdated: true,
  locales: {
    "/": {
      navbar: navbar,
    },
    "/en/": {
      navbar: [
        {
          text: "Docs",
          icon: "creative",
          link: "/main/",
        },
        {
          text: "Update",
          icon: "creative",
          link: "/update/",
        },
        {
          text: "Links",
          icon: "creative",
          children: [
            {
              text: "Nonebot2 HomePage",
              icon: "creative",
              link: "https://nb2.baka.icu/",
            },
            {
              text: "Novelai Bot(koishi) Docs",
              icon: "creative",
              link: "https://bot.novelai.dev/",
            },
            {
              text: "About Senanana",
              icon: "creative",
              link: "https://github.com/sena-nana",
            },
          ],
        },
      ],
    }
  },
  sidebar: {
    "/main/": "structure",
    "/update/": "structure",
  },
  footer: "后面没有了哦~",
  displayFooter: true,
  copyright:
    "MIT Licensed / CC-BY-NC-SA | Copyright © 2022-present 星奈奈奈 Senanana",
  pageInfo: ["Author", "ReadingTime", "Word"],
  encrypt: {
    config: {
      "/guide/encrypt.html": ["1234"],
    },
  },
  plugins: {
    git: {
      updatedTime: true,
      contributors: true,
      createdTime: false,
    },
    photoSwipe: {},
    pwa: {
      showInstall: true,
    },
    sitemap: {},
    mdEnhance: {
      gfm: true,
      container: true,
      tabs: true,
      codetabs: true,
      align: true,
      tasklist: true,
      flowchart: true,
      stylize: [],
      presentation: false,
    },
  },
});
