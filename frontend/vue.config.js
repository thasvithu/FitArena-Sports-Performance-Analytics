const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: ['vuetify'],
  lintOnSave: false, // Disable ESLint during serve
  
  devServer: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },

  pluginOptions: {
    vuetify: {
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    }
  },

  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'FitArena - Sports Performance Analytics'
      return args
    })
  }
})
