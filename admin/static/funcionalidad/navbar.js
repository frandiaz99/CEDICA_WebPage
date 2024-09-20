new Vue({
    el: '#app',
    data: {
        dropdownOpen: false
    },
    methods: {
        toggleDropdown() {
            this.dropdownOpen = !this.dropdownOpen;
        }
    }
});

