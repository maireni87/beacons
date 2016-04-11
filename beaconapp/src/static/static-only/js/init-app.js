yield Request(url, self.parse_result, meta={
    'splash': {
        'args': {
            # set rendering arguments here
            'html': 1,
            'png': 1,

            # 'url' is prefilled from request url
        },

        # optional parameters
        'endpoint': 'render.json',  # optional; default is render.json
        'splash_url': '<url>',      # overrides SPLASH_URL
        'slot_policy': scrapyjs.SlotPolicy.PER_DOMAIN,
    }
})