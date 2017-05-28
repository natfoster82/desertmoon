(function () {
    var socket;
    var md;
    var vm = new Vue({
        el: '#app',
        data: {
            logs: [],
            command: '',
            cachedCommands: [],
            socket: socket,
            prompt: null,
            subject: '',
            promptResponses: {},
            room: GLOBALS.room,
            handle: GLOBALS.handle
        },
        methods: {
            submit: function () {
                if (!vm.command.length) return;
                var payload = {
                    room: vm.room,
                    handle: vm.handle,
                    subject: vm.subject,
                    prompt_responses: vm.promptResponses
                };
                if (vm.prompt) {
                    vm.promptResponses[vm.prompt.key] = vm.command;
                } else {
                    vm.cachedCommands.unshift(vm.command);
                }
                payload.command = vm.cachedCommands[0].toLowerCase();
                socket.emit('submit', payload, function(data){
                    vm.room = data['room'];
                    vm.subject = data['subject'];
                    vm.prompt = data['prompt'];
                    if (!vm.prompt) {
                        vm.promptResponses = {};
                    }
                    vm.command = data['default'];
                    vm.handle = data['handle'];
                });
            },
            renderMarkdown: function (text) {
                console.log('rendering');

            }
        }
    });

    function init () {
        md = window.markdownit();
        socket = io();
        socket.on('log', function (log) {
            log.html = md.render(log.text);
            vm.logs.push(log);
        });
        socket.on('connect', function() {
            socket.emit('join_room', vm.room)
        });
        socket.emit('launch', {'handle': vm.handle});
    }
    init();
})();
