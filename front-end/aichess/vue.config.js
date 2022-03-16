const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = 'A five-in-a-row Game with AI!'
        return args
      })
  },
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production'
    ? './'
    : './'
})
