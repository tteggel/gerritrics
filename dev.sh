while true; do (gerritrics -a 0.0.0.0 -p 8080 -m 10.10.10.2 &) && inotifywait -qre modify,create /var/lib/gerritrics; killall gerritrics; done
