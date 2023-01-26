import { defineUserConfig } from "vuepress";
import theme from "./theme";
import { searchProPlugin } from "vuepress-plugin-search-pro";
export default defineUserConfig({
  locales: {
    "/": { lang: "zh-CN" },
    "/en/": { lang: "en-US" },
  },

  title: "nonebot-plugin-novelai",
  description: "基于Nonebot的novelai使用说明书",
  theme,
  shouldPrefetch: false,
  plugins: [
    searchProPlugin({
      locales: {
        "/": {
          placeholder: "搜索",
        },
        "/en/": {
          placeholder: "Search",
        },
      },
      indexContent: true,
    }),
  ],
});
