module.exports = {
  apps : [{
    name: 'DutyBot',
    script: 'app.py',
    autorestart: false,
    watch: true,
    pid: '/path/to/pid/file.pid',
    interpreter: 'python3',
    max_restarts: 10,
    ignore_watch: ["logs", ".vscode"],
  }, {
    name: 'echo-python-3',
    cmd: 'hello.py',
    interpreter: 'python3'
  }],

  deploy : {
    production : {
      user : 'root',
      host : 'localhost',
      ref  : 'origin/master',
      repo : 'https://github.com/drykov-ttc/support_bot.git',
      path : '/opt/dutyBot',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};
