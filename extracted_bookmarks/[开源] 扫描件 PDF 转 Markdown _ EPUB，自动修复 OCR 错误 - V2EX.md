# [开源] 扫描件 PDF 转 Markdown / EPUB，自动修复 OCR 错误 - V2EX

**原始链接**: https://www.v2ex.com/t/1120037#reply13
**提取时间**: 2025-07-28 10:23:18

---

æœ€è¿‘æˆ‘ä»¬å¼€æº�äº†ä¸€ä¸ª PDF å¤„ç�†å·¥å…· - [pdf-craft](https://github.com/oomol-lab/pdf-craft)ï¼Œä¸“æ³¨äº�è§£å†³æ‰«æ��ä¹¦ç±� PDF è½¬æ�¢çš„ç—›ç‚¹ï¼Œè®©ä¹¦ç±�æ•°å­—åŒ–æ›´æ™ºèƒ½ã€‚pdf-craft æ”¯æŒ�å°† PDF è½¬ä¸º Markdown å’Œ EPUB ï¼Œæ™ºèƒ½å¤„ç�†æ–‡æœ¬ã€�å›¾è¡¨ã€�å…¬å¼�ç­‰å†…å®¹ï¼Œé€‚ç”¨äº�æŠ€æœ¯æ–‡æ¡£ã€�ä¹¦ç±�æ•°å­—åŒ–ã€�è®ºæ–‡ç ”ç©¶ç­‰åœºæ™¯ã€‚

## ç—›ç‚¹ä¸�è§£å†³æ–¹æ¡ˆ

  * **PDF ä¸�ä¾¿äº�ç§»åŠ¨è®¾å¤‡é˜…è¯»** ï¼šå°† PDF è½¬ä¸º EPUB ï¼Œé€‚é…�å�„ç§�å±�å¹•å¤§å°�
  * **ä¹¦ç±�ç»“æ�„æ··ä¹±** ï¼šæ™ºèƒ½åˆ†æ��ç« èŠ‚ã€�ç›®å½•ï¼Œé‡�å»ºç»“æ�„åŒ–å†…å®¹
  * **æ³¨é‡Šå’Œå¼•ç”¨éš¾ä»¥è¿½è¸ª** ï¼šä½¿ç”¨ LLM æ™ºèƒ½å¤„ç�†æ³¨é‡Šå’Œå¼•ç”¨
  * **OCR è¯†åˆ«é”™è¯¯å¤š** ï¼šç»“å�ˆ LLM è‡ªåŠ¨çŸ«æ­£è¯†åˆ«é”™è¯¯
  * **æ‰«æ��ä»¶ PDF éš¾ä»¥è¢« AI ã€�ä»£ç �å¤„ç�†** ï¼šåˆ†æ��å¹¶ç»“æ�„åŒ– PDF æ‰«æ��ä»¶ï¼Œä»¥ä¾› AI ã€�ä»£ç �è¯»å�–



## ä¸»è¦�ç‰¹æ€§

  * **PDF è½¬ Markdown**

    * çº¯æœ¬åœ°è¿�è¡Œï¼ŒGPU åŠ é€Ÿæ”¯æŒ�
    * æ™ºèƒ½è¿‡æ»¤é¡µçœ‰é¡µè„šç­‰æ— å…³å…ƒç´ 
    * è‡ªåŠ¨å¤„ç�†è·¨é¡µæ–‡æœ¬é¡ºæ�¥
    * å›¾è¡¨ã€�å…¬å¼�è‡ªåŠ¨æ��å�–ä¸ºå›¾ç‰‡
  * **PDF è½¬ EPUB**

    * æ™ºèƒ½æ�„å»ºä¹¦ç±�ç»“æ�„å’Œç›®å½•
    * æ��å�–å¹¶ä¿�ç•™æ³¨é‡Šå’Œå¼•ç”¨ï¼Œå¹¶åœ¨ EPUB ä¸­ä»¥å�ˆé€‚çš„æ–¹å¼�é‡�æ–°ç»„ç»‡
    * æ”¯æŒ�ä¸­æ–­æ�¢å¤�åˆ†æ��
    * LLM è¾…åŠ©æ ¡æ­£ OCR é”™è¯¯
  * **æŠ€æœ¯äº®ç‚¹**

    * ç»“å�ˆ [DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO) å¸ƒå±€åˆ†æ��
    * ä½¿ç”¨ [OnnxOCR](https://github.com/jingsongliujing/OnnxOCR) è¿›è¡Œæ–‡æœ¬è¯†åˆ«
    * é›†æˆ� [layoutreader](https://github.com/ppaanngggg/layoutreader) ä¼˜åŒ–é˜…è¯»é¡ºåº�
    * å�¯æ�¥å…¥ DeepSeek ç­‰ LLM æœ�åŠ¡



## æŠ€æœ¯ç»†èŠ‚

é¡¹ç›®åŸºäº� Python å¼€å�‘ï¼Œå�¯é€šè¿‡ pip å®‰è£…ï¼š
    
    
    pip install pdf-craft
    

æ ¸å¿ƒä½¿ç”¨æ–¹æ³•ç¤ºä¾‹ï¼š
    
    
    # PDF è½¬ Markdown ï¼ˆçº¯æœ¬åœ°å¤„ç�†ï¼‰
    from pdf_craft import PDFPageExtractor, MarkDownWriter
    
    extractor = PDFPageExtractor(
      device="cuda:0",  # GPU åŠ é€Ÿ
      model_dir_path="/path/to/model/dir/path",
    )
    with MarkDownWriter(markdown_path, "images", "utf-8") as md:
      for block in extractor.extract(pdf="/path/to/pdf/file"):
        md.write(block)
    

å¯¹äº�æ›´å¤�æ�‚çš„ EPUB è½¬æ�¢ï¼Œå�¯ä»¥æ�¥å…¥ LLMï¼š
    
    
    from pdf_craft import LLM, analyse, generate_epub_file
    
    # é…�ç½® LLM
    llm = LLM(
      key="sk-XXXXX",
      base_url="https://api.deepseek.com",
      model="deepseek-chat",
      token_encoding="o200k_base",
    )
    
    # åˆ†æ�� PDF
    analyse(
      llm=llm,
      pdf_page_extractor=extractor,
      pdf_path="/path/to/pdf/file",
      analysing_dir_path="/path/to/temp",
      output_dir_path="/path/to/output",
    )
    
    # ç”Ÿæˆ� EPUB
    generate_epub_file(
      from_dir_path="/path/to/output",
      epub_file_path="/path/to/book.epub",
    )
    

## å®�é™…æ•ˆæ�œ

![](https://i.v2ex.co/WO2VDN5I.png)

![](https://i.v2ex.co/A1hA4jNL.png)

![](https://i.v2ex.co/bVONPcyN.png)

## ç«‹å�³ä½“éªŒï¼Œæ— éœ€ç�¯å¢ƒé…�ç½®

æƒ³å¿«é€Ÿå°�è¯• pdf-craft è€Œä¸�æƒ³æŠ˜è…¾ç�¯å¢ƒé…�ç½®ï¼Ÿæˆ‘ä»¬æ��ä¾›äº†æ›´ç®€å�•çš„æ–¹å¼�ï¼š **ä½¿ç”¨ OOMOL Studio ä¸€é”®ä½“éªŒ** ï¼š[pdf-craft for OOMOL studio](https://hub.oomol.com/package/pdf-craft)

[OOMOL Studio](https://oomol.com/) æ˜¯æˆ‘ä»¬å¼€å�‘çš„å·¥ä½œæµ� IDE ï¼Œå†…ç½®äº†éš”ç¦»çš„è¿�è¡Œç�¯å¢ƒï¼Œæ— éœ€å¤�æ�‚é…�ç½®ï¼Œå�³å�¯ç«‹å�³ä½“éªŒ pdf-craft çš„å…¨éƒ¨åŠŸèƒ½ã€‚ å…³äº� OOMOL Studio å�¯ä»¥æŸ¥çœ‹ä¹‹å‰�çš„ä»‹ç»�: [ä¸€æ¬¾å…¨æ–°çš„å·¥ä½œæµ� IDE](https://v2ex.com/t/1112879)ã€‚

å½“ç„¶ï¼Œpdf-craft ä»�ç„¶å®Œå…¨å¼€æº�ï¼Œä½ ä¾�ç„¶å�¯ä»¥æŒ‰ç…§ä¸Šè¿°æ–¹æ³•åœ¨è‡ªå·±çš„ç�¯å¢ƒä¸­é…�ç½®ä½¿ç”¨ã€‚

## é€‚ç”¨åœºæ™¯

  * **æŠ€æœ¯æ–‡æ¡£é˜…è¯»** ï¼šå°†ç¹�æ�‚çš„æŠ€æœ¯æ–‡æ¡£è½¬ä¸ºç»“æ�„åŒ–å†…å®¹
  * **ä¹¦ç±�æ•°å­—åŒ–** ï¼šæŠŠçº¸è´¨æ‰«æ��ä¹¦è½¬ä¸ºä¾¿æ�ºçš„ç”µå­�ä¹¦
  * **è®ºæ–‡ç ”ç©¶** ï¼šå¿«é€Ÿæ��å�–è®ºæ–‡å†…å®¹å¹¶æ–¹ä¾¿å¼•ç”¨
  * **å­¦ä¹ æ��æ–™æ•´ç�†** ï¼šå°†è¯¾ç¨‹è®²ä¹‰å¤„ç�†ä¸ºæ˜“äº�å­¦ä¹ çš„æ ¼å¼�
  * **ä»£ç �æ–‡æ¡£æ��å�–** ï¼šä»� PDF æ•™ç¨‹ä¸­æ��å�–å�¯ç”¨ä»£ç �



## å¼€æº�ä¸�ç¤¾åŒº

é¡¹ç›®åˆšåˆšèµ·æ­¥ï¼Œæˆ‘ä»¬é��å¸¸æ¬¢è¿�å�„ä½� V å�‹å�‚ä¸�ï¼š

  * GitHub åœ°å�€ï¼š<https://github.com/oomol-lab/pdf-craft>
  * é—®é¢˜å��é¦ˆï¼š<https://github.com/oomol-lab/pdf-craft/issues>
  * æ¼”ç¤ºè§†é¢‘ï¼š[Bilibili é“¾æ�¥](https://www.bilibili.com/video/BV1tMQZY5EYY/)



å¦‚æ�œè§‰å¾—ä¸�é”™ï¼Œæ¬¢è¿�ç»™é¡¹ç›®ç‚¹ä¸ª star â­�ï¼Œæœ‰ä»€ä¹ˆæƒ³æ³•ä¹Ÿå�¯ä»¥åœ¨è¯„è®ºåŒºäº¤æµ�ï¼Œæˆ–è€…æ��äº¤ PR ä¸€èµ·å®Œå–„è¿™ä¸ªå·¥å…·ã€‚

ä½ ä¹Ÿå�¯ä»¥é€šè¿‡ <https://oomol.com/community/> æ‰¾åˆ°æˆ‘ä»¬ã€‚
