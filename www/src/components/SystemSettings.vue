<template>
<div id="system-settings">
    <vue-headful title="Settings"/>
    <h1>System preference</h1>
    <div class="flex-grid">
      <div>
          <h2>Background Color</h2>
           <el-color-picker class="pick_color" @change="background"></el-color-picker>
      </div>
    </div>
</div>
</template>

<script>
export default {
    name: 'system-settings',
    data () {
        return {

        }
    },
    methods: {
        background(color){
            document.getElementsByTagName('main')[0].style.background = color
        }
    }
}
</script>