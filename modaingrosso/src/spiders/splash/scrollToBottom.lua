function main(splash)
  local num_scrolls = 10
  local scroll_delay = 1

  local scroll_to = splash:jsfunc("window.scrollTo")
  local get_body_height = splash:jsfunc(
      "function() {return document.body.scrollHeight;}"
  )
  splash:init_cookies(splash.args.cookies)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))

  for _ = 1, num_scrolls do
      scroll_to(0, get_body_height())
      splash:wait(scroll_delay)
  end
  return {
    png = splash:png(),
    html=splash:html(),
    cookies=splash:get_cookies()
  }
end