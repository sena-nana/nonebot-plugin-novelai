import { defineUserConfig } from "vuepress";
import theme from "./theme";
import { searchPlugin } from "@vuepress/plugin-search";
export default defineUserConfig({
    lang: "zh-CN",
    title: "nonebot-plugin-novelai",
    description: "基于Nonebot的novelai使用说明书",
  theme,
  shouldPrefetch: false,
  plugins:[
    searchPlugin({
      locales: {
        '/': {
          placeholder: '搜索',
        },},
      isSearchable: (page) => page.path !== '/',   
    }),
  ],
});
