function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))

  local usernameInput = splash:select('body > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=text]')
  local usernameInputBounds = usernameInput:bounds()
  local passwordInput = splash:select('body > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(5) > td:nth-child(2) > input[type=password]')
  local passwordInputBounds = passwordInput:bounds()
  local confirmBtn = splash:select('body > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(9) > td > table > tbody > tr > td:nth-child(2) > input[type=image]')
  local confirmBtnBounds = confirmBtn:bounds()

  assert(usernameInput:mouse_click{x=usernameInputBounds.width/3, y=usernameInputBounds.height/3})
  splash:wait(0.5)
  assert(usernameInput:send_keys('email@email.com'))
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