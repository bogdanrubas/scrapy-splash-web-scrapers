function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))

  -- czeka na pojawienie sie modalu
  splash:wait(8)

  local closeModal = splash:select('.spu-icon')
  local closeModalBounds = closeModal:bounds()

  assert(closeModal:mouse_click{x=closeModalBounds.width/3, y=closeModalBounds.height/3})
  splash:wait(5)

  local usernameInput = splash:select('input#username')
  local usernameInputBounds = usernameInput:bounds()
  local passwordInput = splash:select('input#password')
  local passwordInputBounds = passwordInput:bounds()
  local confirmBtn = splash:select('p.form-footer > button')
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