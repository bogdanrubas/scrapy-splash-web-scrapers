function main(splash)
  splash:set_user_agent(splash.args.ua)
  splash:init_cookies(splash.args.cookies)
  assert(splash:go(splash.args.url))
  splash:wait(3)

  local usernameInput = splash:select('input#Email')
  local usernameInputBounds = usernameInput:bounds()
  local passwordInput = splash:select('input#Password')
  local passwordInputBounds = passwordInput:bounds()
  local confirmBtn = splash:select('form > div.buttons > input.login-button')
  local confirmBtnBounds = confirmBtn:bounds()

  assert(usernameInput:mouse_click{x=usernameInputBounds.width/3, y=usernameInputBounds.height/3})
  splash:wait(0.5)
  assert(usernameInput:send_keys('youremail@gmail.com'))
  splash:wait(0.5)
  assert(passwordInput:mouse_click{x=passwordInputBounds.width/3, y=passwordInputBounds.height/3})
  splash:wait(0.5)
  assert(passwordInput:send_keys('pwd'))
  splash:wait(0.5)
  assert(confirmBtn:mouse_click{x=confirmBtnBounds.width/3, y=confirmBtnBounds.height/3})
  splash:wait(3)

  return {
    png = splash:png(),
    html=splash:html(),
    cookies=splash:get_cookies()
  }
end