function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))

  while not splash:select('.topbar-menu-container .nasa-login-register-ajax') do
    splash:wait(0.1)
  end

  local loginBtn = splash:select('.topbar-menu-container .nasa-login-register-ajax')
  local loginBtnBounds = loginBtn:bounds()
  local usernameInput = splash:select('#nasa_username')
  local usernameInputBounds = usernameInput:bounds()
  local passwordInput = splash:select('#nasa_password')
  local passwordInputBounds = passwordInput:bounds()
  local confirmBtn = splash:select('.row-submit > .button')
  local confirmBtnBounds = confirmBtn:bounds()

  splash:wait(3)
  assert(loginBtn:mouse_click{x=loginBtnBounds.width/3, y=loginBtnBounds.height/3})
  splash:wait(2)
  assert(usernameInput:mouse_click{x=usernameInputBounds.width/3, y=usernameInputBounds.height/3})
  splash:wait(0.5)
  assert(usernameInput:send_keys('youremail@email.com'))
  splash:wait(0.5)
  assert(passwordInput:mouse_click{x=passwordInputBounds.width/3, y=passwordInputBounds.height/3})
  splash:wait(0.5)
  assert(passwordInput:send_keys('yourpassword'))
  splash:wait(0.5)
  assert(confirmBtn:mouse_click{x=confirmBtnBounds.width/3, y=confirmBtnBounds.height/3})
  splash:wait(5)

  return {
    png = splash:png(),
    html=splash:html(),
    cookies=splash:get_cookies()
  }
end