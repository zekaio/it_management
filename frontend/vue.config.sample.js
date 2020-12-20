module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/path/to/project' : '/',
  productionSourceMap: false,
  chainWebpack: (config) => {
    config.resolve.symlinks(true); // 修复热更新失效
  },
};
