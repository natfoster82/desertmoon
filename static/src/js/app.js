(function () {
    function init () {
        socket.on('log', function (log) {
            vm.logs.push(log);
        });
        socket.on('room', function (room) {
            vm.room = room;
        });
    }
    var socket = io();

    var vm = new Vue({
        el: '#app',
        data: {
            logs: [],
            command: '',
            cachedCommands: [],
            socket: socket,
            isPrompt: false,
            promptCallback: function(){},
            room: null,
            handle: '(Anon)'
        },
        methods: {
            submit: function () {
                if (!this.command.length) return;
                var payload = {
                    room: this.room
                };
                var doEmit = true;
                if (this.isPrompt) {
                    this.promptCallback();
                    payload.handle = this.handle;
                    payload.command = this.cachedCommands[0].toLowerCase();
                    this.promptCallback = function () {};
                    this.isPrompt = false;
                } else {
                    payload.handle = this.handle;
                    payload.command = this.command.toLowerCase();
                    this.cachedCommands.unshift(this.command);
                    var verb = this.command.split(' ')[0].toLowerCase();
                    // todo: pull this out into an interceptor method if we get too many prompt cases
                    if (verb === 'init' || verb === 'join') {
                        this.isPrompt = true;
                        this.logs.push({
                            handle: 'Server',
                            timestamp: '',
                            text: 'What is your operator handle?'
                        });
                        this.promptCallback = this.setHandle;
                        doEmit = false;
                    }
                }
                if (doEmit) {
                    socket.emit('submit', payload);
                }
                this.command = '';
            },
            setHandle: function () {
                this.handle = this.command;
            }
        }
    });

    init();
})();
