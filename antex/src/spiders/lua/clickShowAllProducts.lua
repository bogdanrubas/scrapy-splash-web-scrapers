function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))


  local showAllButton = splash:select('.showall button')
  local bounds = showAllButton:bounds()
  assert(showAllButton:mouse_click{x=bounds.width/3, y=bounds.height/3})
  splash:wait(30)

  return {
    html=splash:html()
  }
end