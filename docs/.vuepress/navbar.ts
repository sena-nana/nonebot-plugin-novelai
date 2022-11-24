import { navbar } from "vuepress-theme-hope";

export default navbar([
  { 
    text: "使用手册", 
    icon: "creative", 
    link: "/main/", 
  },
  { 
    text: "更新日志", 
    icon: "creative", 
    link: "/update/", 
  },
  { 
    text: "友链", 
    icon: "creative", 
    children: [
      {
        text: "Nonebot2主页", 
        icon: "creative", 
        link: "https://nb2.baka.icu/", 
      },
      {
        text: "Novelai Bot说明书", 
        icon: "creative", 
        link: "https://bot.novelai.dev/", 
      },
      {
        text: "MagiaHonkai", 
        icon: "markdown", 
        link: "https://sena-nana.github.io/", 
      },
      {
        text: "关于星奈", 
        icon: "creative", 
        link: "https://github.com/sena-nana", 
      },
    ],
  },
]);
