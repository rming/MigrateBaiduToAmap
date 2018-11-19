# MigrateBaiduToAmap

### unknown error: Element ... is not clickable at point##

被反爬虫，出现了验证码

```python
Traceback (most recent call last):
  File "./baidu.py", line 140, in <module>
    handler.run()
  File "./baidu.py", line 45, in run
    poiId and self.addAmapFav(poiId)
  File "./baidu.py", line 118, in addAmapFav
    btn and btn.click()
  File "/Library/Python/2.7/site-packages/splinter/driver/webdriver/__init__.py", line 634, in click
    self._element.click()
  File "/Library/Python/2.7/site-packages/selenium/webdriver/remote/webelement.py", line 80, in click
    self._execute(Command.CLICK_ELEMENT)
  File "/Library/Python/2.7/site-packages/selenium/webdriver/remote/webelement.py", line 633, in _execute
    return self._parent.execute(command, params)
  File "/Library/Python/2.7/site-packages/selenium/webdriver/remote/webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "/Library/Python/2.7/site-packages/selenium/webdriver/remote/errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.WebDriverException: Message: unknown error: Element <span class="collect favit">...</span> is not clickable at point (81, 352). Other element would receive the click: <div class="sufei-dialog-mask"></div>
  (Session info: chrome=70.0.3538.102)
  (Driver info: chromedriver=2.43.600229 (3fae4d0cda5334b4f533bede5a4787f7b832d052),platform=Mac OS X 10.13.6 x86_64)
```
