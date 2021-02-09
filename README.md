# translationshortcut

## Automatically substitute translations for surveymonkey

- 注意顺序：尽量先多语言后build问卷，如果不能，尽量保证所有问卷内的改动都反映到多语言文档里，同一语言下两边内容一致，用复制粘贴的方式更为保险。
- 尽量用简体中文上原版问卷，规避Survey Monkey简体繁体中文的bug，如果不能，用英文上完之后可手动改一下。
- 在包没有做好前，可以右键-显示包内容-Contents-MacOS-TranslationSub，这样打开
- 翻译目标语言可以直接复制粘贴Excel文档中的，空格隔开就行，无论多少空格都没关系。
- 如果有没有上上去的多语言：
  - 先检查是不是有对应问题，可以靠复制粘贴让monkey上和Excel中同一句话完全保持一致。
  - 如果原文卷中没上上去的句子中有大于小于号，且有部分文字，可能会薛定谔地导致出错，问题待查。
