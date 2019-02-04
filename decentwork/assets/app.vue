<template id="app">
    <div id="apps">
        <navbar />
        <router-view :key="$route.fullPath"></router-view>
    </div>
</template>