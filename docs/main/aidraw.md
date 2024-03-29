---
title: 使用
icon: markdown
order: 1
tag:
  - Markdown
---

## 指令开头

每个指令都需要严格使用规定的开头，这样 BOT 才能够识别到你的命令

插件标准的开头为 **.aidraw** 例如：

```
.aidraw 可爱的萝莉
```

除了.aidraw，你还可以使用 **绘画** , **咏唱** , **召唤**, **约稿** 以及不带"."的 **aidraw**，例如 (以下指令都是可以正常运行的)：

```
.aidraw 可爱的萝莉
绘画 超可爱的萝莉
咏唱 非常可爱的萝莉
召唤 cute loli
约稿 loli,cute
aidraw loli,可爱
```

需要注意的是，Nonebot 在 Env 中可以自定义指令的开头，这就使得你必须先输入 Env 中指定的开头，再输入插件的指令开头才能够识别到，假如你的 Env 中设置了指令以#起始，那么就需要输入#.aidraw 才能够触发 (或者#aidraw，备用指令中的 aidraw 就是为了这种情况而存在的)

## 基础用法

### 从文本生成图片 (txt2img)

输入指令开头[.aidraw]加上关键词描述即可，指令开头和关键词之间以空格分开

```
.aidraw 可爱的萝莉
```

![.aidraw 可爱的萝莉](./images/t2i.png)
::: info
插件内置了 H 屏蔽词，并默认启动。包含屏蔽词的指令会被默认拒绝，即便你打中文也是如此
:::

### 从图片生成图片 (img2img)

::: warning
此功能在 novelai_paid 设置为 0 时无法使用
:::

1. 在以文本生图的基础上，将图片加入到消息中即可自动切换至图片生图
   ![.aidraw 可爱的萝莉 [图片]](./images/i2i1.png)
2. 回复带有图片的消息，并以正常方式调用即可自动切换至图片生图
   ![[图片] .aidraw 可爱的萝莉](./images/i2i2.png)

## 关键词 (tags)

使用关键词描述你想要的图像。多个关键词之间用逗号分隔。每一个关键词也可以由多个单词组成，单词之间可以用空格或下划线分隔。插件能够自动识别关键词中的中文部分，并将其翻译为英语。为了翻译能够更加准确，如果你想要混输中英文，请将中文和英文之间用逗号分开

nonebot-plugin-novelai 会保留关键词中包含的语法，不会进行转换。因此只要后台支持，各种影响因子的语法均会正常发挥作用

### 负面关键词 (ntags)

使用 **-u** 、 **--ntags** 或 **-排除** 以添加负面关键词，避免生成不需要的内容。例如：

```
.aidraw 可爱的萝莉 --ntags nsfw
```

### 影响因子

使用 **半角方括号 []** 包裹关键词以减弱该关键词的权重，使用 **半角花括号 {}** 包裹关键词以增强该关键词的权重。可以通过多次使用括号来进一步强调关键词。例如：

```
.aidraw [cute],{loli},{{kawaii}}} --ntags nsfw
```

在 Stable Diffusion 中，还可以通过 **半角圆括号 ()**来增强权重，相比于花括号，圆括号增加的权重要小

::: info
除了影响因子外，关键词的顺序也会对生成结果产生影响。越重要的词应该放到越前面。插件的内置优化词条会默认放置最前方，基础词条会添加至其后
:::

### 要素混合

使用 **| (shift+\\)** 分隔多个关键词以混合多个要素。例如：

```
.aidraw black hair|white hair,loli
```

你将得到一只缝合怪 (字面意义上)。但是某些情况下可能会产生意外奇妙的效果。

可以进一步在关键词后添加 :x 来指定单个关键词的权重，x 的取值范围是 0.1~100，默认为 1。例如：

```
.aidraw black hair:2|white hair,loli
```

实际上，x 的取值支持-1~-0.1 的范围，这会在图片中让对应的元素消失 (变黑)，而-1 时将会得到完全的黑色。这是一个未经过严谨测试的功能，仅在 novelai 官方帮助中被简单提及。

### 基础关键词

nonebot-plugin-novelai 允许 BOT 主配置基础的正面和负面词条，它们会在请求时被添加在结尾，具体如何配置见[设置](./config.md)一节

群主和管理员可以通过管理指令来设置仅在本群生效的基础关键词，具体如何配置见[管理](./manager.md)一节

如果想要手动忽略这些基础关键词，可以使用 **-o**、**--override** 或 **-不优化** 参数。

## 高级用法

### 设置分辨率 (resolution)

可以用 **-r** 、 **--resolution** 或 **-形状** 更改图片分辨率，插件内内置了部分预设，包括：

- **square**:640x640，可以使用**s**或者**方**代替
- **portrait**:512x768，可以使用**p**或者**高**代替
- **landscape**:768x512，可以使用**l**或者**宽**代替

```
.aidraw cute,loli -r p
```

同样地，你可以使用 x 分割宽高，来自定义分辨率：

```
.aidraw cute,loli -r 1024x1024
```

::: info
由于 Novelai、Naifu 和 Stable Diffusion 的限制，输出图片的长宽都必须是 64 的倍数。当你输入的图片长宽不满足此条件时，我们会自动修改为接近此宽高比的合理数值。
:::
::: info
在 BOT 主限制分辨率的最大值、仅免费模式 这两种情况下，插件会自动按比例降低分辨率以小于限制。最后生成图片的分辨率可能并不与你输入的分辨率一致
:::

### 种子 (seed)

AI 会使用种子来生成噪音然后进一步生成你需要的图片，每次随机生成时都会有一个唯一的种子。使用 **-s** 、 **--seed** 或 **-种子** 并传入相同的种子可以让 AI 尝试使用相同的路数来生成图片。

```
.aidraw cute,loli -s 5201314
```

默认情况下，种子会在 1-4294967295 之间随机取值

### 迭代步数 (steps)

更多的迭代步数可能会有更好的生成效果，但是一定会导致生成时间变长。太多的 steps 也可能适得其反，几乎不会有提高。Stable Diffusion 官方说明中，写着大于 50 的步数不会再带来提升。

默认情况下的迭代步数为 28 (传入图片时为 50)，28 也是不会收费的最高步数。可以使用 **-t** 、 **--steps** 或 **-步数** 手动控制迭代步数。

```
.aidraw cute,loli -t 50
```

### 对输入的服从度 (scale)

服从度较低时 AI 有较大的自由发挥空间，服从度较高时 AI 则更倾向于遵守你的输入。但如果太高的话可能会产生反效果 (比如让画面变得难看)。更高的值也需要更多计算。

有时，越低的 scale 会让画面有更柔和，更有笔触感，反之会越高则会增加画面的细节和锐度。

| 服从度 | 行为                            |
| ------ | ------------------------------- |
| 2~8    | 会自由地创作，AI 有它自己的想法 |
| 9~13   | 会有轻微变动，大体上是对的      |
| 14~18  | 基本遵守输入，偶有变动          |
| 19+    | 非常专注于输入                  |

默认情况下的服从度为 11。可以使用 **-c** 、 **--scale** 或 **-服从** 手动控制服从度。

```
.aidraw cute,loli -c 10
```

### 强度 (strength)

::: info
该参数仅会在以图生图时发挥作用
:::
AI 会参考该参数调整图像构成。值越低越接近于原图，越高越接近训练集平均画风。使用 **-e** 、 **--strength** 或 **-强度** 手动控制强度。

| 使用方式         | 推荐范围 |
| ---------------- | -------- |
| 捏人             | 0.3~0.7  |
| 草图细化         | 0.2      |
| 细节设计         | 0.2~0.5  |
| 装饰性图案设计   | 0.2~0.36 |
| 照片转背景       | 0.3~0.7  |
| 辅助归纳照片光影 | 0.2~0.4  |

以上取值范围来自微博画师帕兹定律的[这条微博](https://share.api.weibo.cn/share/341911942,4824092660994264.html)

个人在使用中，如果是用来生成对应姿势和大致样子的角色来获取人设灵感，会拉到 0.6~0.8。
### 噪声 (noise)
::: info
该参数仅会在以图生图时发挥作用
:::
噪声是让 AI 生成细节内容的关键。更多的噪声可以让生成的图片拥有更多细节，但是太高的值会让产生异形，伪影和杂点。

如果你有一张有大片色块的草图，可以调高噪声以产生细节内容，但噪声的取值不宜大于强度。当强度和噪声都为 0 时，生成的图片会和原图几乎没有差别。

使用 **-n** 、 **--noise** 或 **-噪声** 手动控制噪声。
### 数量 (batch)
顾名思义，数量就是同时生成多少张。在插件中，无论数量设置为多少，都是一张一张生成，最后再统一发送。即便如此，在点数模式中还是会将同时生成多张图认作消耗点数的情况。

在设置中，BOT主能够设置同时生成的最大数量，默认为3。当用户设置的值超出了最大数量，会被限制。

使用 **-b** 、 **--batch** 或 **-数量** 手动控制同时生成数量。

## 特殊处理

如果你的指令中包含"<>"或其他可能会被shell解析器解析掉的符号，请用单引号将其包裹起来，双引号并不能保证例如"\"等字符能够绕过解析