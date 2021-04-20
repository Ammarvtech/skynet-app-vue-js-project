<template>
    <div id="mobile-bar">
        <quick-menu :menu-count=count :icon-class=icons :menu-url-list=list :background-color=backgroundColor :color=color :position=position style="z-index: 999;"></quick-menu>
        <!--<quick-menu :menu-count=getCount :icon-class=icons :menu-url-list=list :background-color=backgroundColor :color=color :position=position :is-open-new-tab=getIsOpenNewTab @process=print></quick-menu>-->
    </div>
</template>

<script>
    import quickMenu from 'vue-quick-menu'

    export default {
        name: "MobileBar",
        components: {
            'quickMenu': quickMenu
        },
        data() {
            return {
                count: 4,
                icons: ["fa fa-usd", "fa fa-globe", "fa fa-sellsy", "fa fa-bar-chart"],
                //icons: ["fa fa-usd", "fa fa-globe", "fa fa-cube", "fa fa-bar-chart", "fa fa-clock-o", "fa fa-line-chart", "fa fa-check"],
                list: [
                    {'isLink': true, url: "/revenue-new"},
                    {'isLink': true, url: "/websites-dfp"},
                    {'isLink': true, url: "/realtime"},
                    {'isLink': true, url: '/campaigns'},
                    // {'isLink': true, url: '/broker'},
                    // {'isLink': true, url: '/optimization'},
                    // {'isLink': true, url: '/validation'}
                ],
                backgroundColor: '#409EFF',
                color: '#ffffff',
                position: 'bottom-left',
                isOpenNewTab: false

            }
        },
        methods: {},
    }
</script>

<style scoped>
</style>