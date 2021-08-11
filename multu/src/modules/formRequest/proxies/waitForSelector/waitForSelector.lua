function main(splash)
  splash:on_request(function(request)
    -- request:set_proxy{
    --   host = '178.128.91.35',
    --   port = 44344,
    -- }
    request:set_proxy{
      host = splash.args.ip,
      port = splash.args.port,
    }
  end)

  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))

  while not splash:select(splash.args.cssSelector) do
    splash:wait(0.1)
  end

  return {html=splash:html()}
end