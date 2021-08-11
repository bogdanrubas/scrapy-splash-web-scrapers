function main(splash)
  splash:set_user_agent(splash.args.ua)
  splash:init_cookies(splash.args.cookies)

  --

  -- splash:on_request(function(request)
  --   blockUrl = "pixel.wp.pl"
  --   url = request.url

  --   if string.find(url, blockUrl) then
  --     request:abort()
  --   end
  -- end)

  --

  assert(splash:go(splash.args.url))

  while not splash:select(splash.args.cssSelector) do
    splash:wait(0.1)
  end

  return {png = splash:png(),html=splash:html(), cookies=splash:get_cookies()}
end