function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))

  local ok, result = splash:with_timeout(function()
    while not splash:select(splash.args.cssSelector) do
      splash:wait(0.1)
    end
  end, splash.args.maxTimeout)

  if not ok then
    if result == "timeout_over" then
      return {
        html=splash:html(),
        isExists=false
      }
    end
  else
      return {
        html=splash:html(),
        isExists=true
      }
  end
end