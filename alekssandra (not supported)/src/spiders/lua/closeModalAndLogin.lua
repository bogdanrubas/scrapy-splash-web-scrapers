function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))

  local usernameInput = splash:select('input#username')
  local usernameInputBounds = usernameInput:bounds()
  local passwordInput = splash:select('input#password')
  local passwordInputBounds = passwordInput:bounds()
  local confirmBtn = splash:select('p.form-footer > button')
  local confirmBtnBounds = confirmBtn:bounds()

  assert(usernameInput:mouse_click{x=usernameInputBounds.width/3, y=usernameInputBounds.height/3})
  splash:wait(0.5)
  assert(usernameInput:send_keys('email@email.com'))
  splash:wait(0.5)
  assert(passwordInput:mouse_click{x=passwordInputBounds.width/3, y=passwordInputBounds.height/3})
  splash:wait(0.5)
  assert(passwordInput:send_keys('pwd123'))
  splash:wait(0.5)
  assert(confirmBtn:mouse_click{x=confirmBtnBounds.width/3, y=confirmBtnBounds.height/3})
  splash:wait(3)

  return {
    png = splash:png(),
    html=splash:html(),
    cookies=splash:get_cookies()
  }
end