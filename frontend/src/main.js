import Vue from 'vue';
import App from './App.vue';
import router from './router';
import {
  Form,
  Button,
  Field,
  Picker,
  Popup,
  Cell,
  CellGroup,
  Image as VanImage,
  Col,
  Row,
  Tabbar,
  TabbarItem,
  GoodsAction,
  GoodsActionIcon,
  GoodsActionButton,
  Icon,
  ActionSheet,
  NavBar,
  List,
  PullRefresh,
  Search,
  Empty,
  Grid,
  GridItem,
  IndexBar,
  IndexAnchor,
  Tab,
  Tabs,
  Sticky,
  Uploader,
} from 'vant';

Vue.config.productionTip = false;

Vue.use(Form)
  .use(Button)
  .use(Field)
  .use(Picker)
  .use(Cell)
  .use(Popup)
  .use(VanImage)
  .use(Col)
  .use(Row)
  .use(CellGroup)
  .use(Tabbar)
  .use(TabbarItem)
  .use(GoodsAction)
  .use(GoodsActionButton)
  .use(GoodsActionIcon)
  .use(Icon)
  .use(ActionSheet)
  .use(NavBar)
  .use(List)
  .use(PullRefresh)
  .use(Search)
  .use(Empty)
  .use(Grid)
  .use(GridItem)
  .use(IndexBar)
  .use(IndexAnchor)
  .use(Tab)
  .use(Tabs)
  .use(Sticky)
  .use(Uploader);

Vue.prototype.$goTo = function(path) {
  this.$router.push({
    path,
  });
};

Vue.prototype.$back = function() {
  this.$router.back();
};

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
