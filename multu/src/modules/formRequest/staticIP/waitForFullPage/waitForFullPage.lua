function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))
  Recheck = true

  Html = splash:html()
  while Recheck == true do
      splash:wait(5)
      Html2 = splash:html()
      if html ~= html2 then

      else
        Recheck = false
        return {
            html = splash:html()
        }
      end
    end
end