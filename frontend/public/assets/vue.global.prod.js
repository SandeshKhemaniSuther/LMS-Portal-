// Vue.js 3 CDN fallback - simplified version
window.Vue = {
    createApp: function(options) {
        return {
            use: function(plugin) { return this; },
            mount: function(selector) {
                console.log('Vue app mounted to', selector);
                return this;
            }
        };
    },
    ref: function(value) { return { value }; },
    createRouter: function(options) {
        return {
            push: function(path) {
                window.location.href = path;
            }
        };
    },
    createWebHistory: function() {
        return function() {};
    }
};

// VueRouter CDN fallback
window.VueRouter = {
    createRouter: window.Vue.createRouter,
    createWebHistory: window.Vue.createWebHistory
};
