function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))
  splash:wait(8)

  return {
    png = splash:png(),
    html=splash:html(),
    cookies=splash:get_cookies()
  }
end