import Vue from "vue";
import App from "./App.vue";
import BootstrapVue from 'bootstrap-vue';
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import VueRouter from "vue-router";
import VueResource from "vue-resource";
import DataTables from 'vue-data-tables';
import Vuetify from 'vuetify'
import VueMediaQueryMixin from 'vue-media-query-mixin';
import vueHeadful from 'vue-headful';
import VeeValidate from 'vee-validate';
import {Laue} from 'laue';
import VueProgressBar from 'vue-progressbar'
import JsonExcel from 'vue-json-excel'
import Snotify from 'vue-snotify';
import VueCookies from 'vue-cookies'
import VDateRange from 'vuetify-daterange-picker';
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import {InputNumber} from 'ant-design-vue';
import VJsoneditor from 'v-jsoneditor';
import vueJsonCompare from 'vue-json-compare';
import vueJsonCool from 'vue-json-cool';

import { MultiSelectPlugin } from "@syncfusion/ej2-vue-dropdowns";
import { MultiSelect, CheckBoxSelection } from '@syncfusion/ej2-dropdowns';


import 'ant-design-vue/dist/antd.css'
import 'vuetify-daterange-picker/dist/vuetify-daterange-picker.css';
import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';

import {store} from './store/store'

const RealTime = () => import(/* webpackChunkName: "RealTime" */ './components/realtime/Campaigns.vue');
const RevenueReport = () => import(/* webpackChunkName: "RevenueReport" */ './components/RevenueReport.vue');
const SystemSettings = () => import(/* webpackChunkName: "SystemSettings" */ './components/SystemSettings.vue');
const DealerStatus = () => import(/* webpackChunkName: "DealerStatus" */ './components/DealerStatus.vue');
const Bidder = () => import(/* webpackChunkName: "BidderSettings" */ './components/Bidder.vue');
const ChangePassword = () => import(/* webpackChunkName: "ChangePassword" */ './components/password/ChangePassword.vue');
const ResetPassword = () => import(/* webpackChunkName: "ResetPassword" */ './components/password/ResetPassword.vue');
const Backstage = () => import(/* webpackChunkName: "Backstage" */ './components/backstage/CreateUser.vue');
const Profiler = () => import(/* webpackChunkName: "Profiler" */ './components/campaigns/Profiler.vue');
const Validation = () => import(/* webpackChunkName: "Validation" */ './components/Validation.vue');
const Factor = () => import(/* webpackChunkName: "Validation" */ './components/Factor.vue');
const DealerActionLog = () => import(/* webpackChunkName: "Log" */ './components/DealerActionLog.vue');
const RTvalidation = () => import(/* webpackChunkName: "Validation" */ './components/RTvalidation.vue');
const WebsitesDFP = () => import(/* webpackChunkName: "Websites" */ './components/websites/CampaignDataDFP.vue');
const WebsitesRT = () => import(/* webpackChunkName: "WebsitesRT" */ './components/realtime/CampaignsRT.vue');
const AlertsSettings = () => import(/* webpackChunkName: "AlertsSettings" */ './components/AlertSettings.vue');
const SiteConfiguration = () => import(/* webpackChunkName: "SiteConfiguration" */ './components/SiteConfiguration.vue');
const ReportDynamic = () => import(/* webpackChunkName: "ReportDynamic" */ './components/ReportDynamic.vue');
const AutomationManagment = () => import(/* webpackChunkName: "AutomationManagment" */ './components/AutomationManagment.vue');


Vue.use(VueCookies);
Vue.use(VDateRange);
Vue.use(VeeValidate, { fieldsBagName: 'veeFields' });
Vue.use(Vuetify);
Vue.use(BootstrapVue);
Vue.use(VueResource);
Vue.use(VueRouter);
Vue.use(ElementUI, {locale});
Vue.use(DataTables);
Vue.use(VueMediaQueryMixin, {framework: 'vuetify'});
Vue.use(Laue);
Vue.use(Snotify);
Vue.use(VueProgressBar, {color: '#2196f3', failedColor: 'red', height: '3px'});
Vue.component('vue-headful', vueHeadful);
Vue.component('downloadExcel', JsonExcel);
Vue.component('VueCtkDateTimePicker', VueCtkDateTimePicker);
Vue.use(InputNumber);
Vue.use(VJsoneditor);
Vue.component('vue-json-compare', vueJsonCompare);
Vue.component('vue-json-cool', vueJsonCool);
Vue.component('sources-dropdown', require('./components/partials/Sources.vue').default);
Vue.component('websites-dropdown', require('./components/partials/Websites.vue').default);
Vue.component('search-box', require('./components/partials/SearchBox.vue').default);
Vue.component('websites-settings-history', require('./components/partials/WebsiteSettingsHistory.vue').default);
Vue.component('websites-multi-dropdown', require('./components/partials/WebsitesMulti.vue').default);
Vue.component('websites-multi-dropdown-checkbox', require('./components/partials/WebsitesMultiCheckbox.vue').default);
MultiSelect.Inject(CheckBoxSelection);
Vue.use(MultiSelectPlugin);

const routes = [
    {path: "/", redirect: '/websites-dfp', name: 'website_dfp'},
    {path: "/realtime", component: RealTime},
    {path: "/alerts", component: AlertsSettings},
    {path: "/dealer", component: DealerStatus},
    {path: "/websites-dfp", component: WebsitesDFP},
    {path: "/websites-rt", component: WebsitesRT},
    {path: "/settings", component: SystemSettings},
    {path: "/ReportDynamic", component: ReportDynamic},
    {path: "/AutomationManagment", component: AutomationManagment},
    {
        path: "/revenue",
        component: RevenueReport,
        beforeEnter: (to, from, next) => {
            store.getters.getUser.settings && store.getters.getUser.settings.enable_revenue == 1 ? next() : next({name: 'website_dfp'});
        }
    },
    {
        path: "/validation",
        component: Validation,
        beforeEnter: (to, from, next) => {
            store.getters.getUser.settings && store.getters.getUser.settings.enable_validation == 1 ? next() : next({name: 'website_dfp'});
        }
    },
    {path: "/factor", component: Factor},
    {path: "/action-log", component: DealerActionLog},
    {path: "/site-configuration", component: SiteConfiguration},
    {path: "/rtvalidation", component: RTvalidation},
    {path: "/campaigns/profiler", component: Profiler},
    {path: "/hb-settings", component: Bidder},
    {path: "/password/change/:code", component: ChangePassword},
    {path: "/password/reset", component: ResetPassword},
    {path: "/backstage", component: Backstage},

];
const router = new VueRouter({
    routes,
    mode: 'hash'
});

new Vue({
    el: "#skynet-dashboard",
    router,
    store,
    render: h => h(App),

});
