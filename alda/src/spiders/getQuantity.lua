function main(splash)
  splash:set_user_agent(splash.args.ua)
  assert(splash:go(splash.args.url))

  local scroll_to = splash:jsfunc("window.scrollTo")
  scroll_to(0, 200)
  local sizes = splash:select_all('.rozmiar > ul li span')
  local returnSizes = {}
  local link_index = 0

  for i, size in ipairs(sizes) do
    local sizes = splash:select_all('.rozmiar > ul li span')
    local sizeBounds = sizes[i]:bounds()
    assert(sizes[i]:mouse_click{x=sizeBounds.width/3, y=sizeBounds.height/3})
    splash:wait(0.5)

    local ok, result = splash:with_timeout(function()
      while not splash:select(".product-prices .old") do
        splash:wait(0.1)
      end
    end, 0.5)

    if not ok then
      if result == "timeout_over" then
        local newPriceElement = splash:select(".product-prices .new")
        local okk, resultt = splash:with_timeout(function()
          while not splash:select(".js-mailalert button") do
            splash:wait(0.1)
          end
        end, 0.5)

        if not okk then
          table.insert(returnSizes, {sizes[i]:text(), newPriceElement:text(), newPriceElement:text(), true})
        else
          table.insert(returnSizes, {sizes[i]:text(), newPriceElement:text(), newPriceElement:text(), false})
        end
      end
    else
        local oldPriceElement = splash:select(".product-prices .old")
        local newPriceElement = splash:select(".product-prices .new")
        local foundEmpty, resultEmpty = splash:with_timeout(function()
          while not splash:select(".js-mailalert") do
            splash:wait(0.1)
          end
        end, 2)

        if not foundEmpty then
          table.insert(returnSizes, {sizes[i]:text(), oldPriceElement:text(), newPriceElement:text(), true})
        else
          table.insert(returnSizes, {sizes[i]:text(), oldPriceElement:text(), newPriceElement:text(), false})
        end
    end
  end

  return {
    png = splash:png(),
    html=splash:html(),
    sizes=returnSizes
  }
end