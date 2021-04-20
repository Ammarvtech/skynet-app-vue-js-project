export default {
    methods: {
        alert(field) {
            this.$alert('Please select ' + field + '', 'Missing field', {
                confirmButtonText: 'OK',
                type: 'warning'
            });
        },
        notice(msg) {
            this.$alert(msg, ' ', {
                confirmButtonText: 'OK',
                type: 'warning',
                customClass: 'notice_msg'
            });
        },
    }
}