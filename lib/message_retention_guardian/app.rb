require "json"
require "webrick"
require_relative "sample_data"
require_relative "analysis"

module MessageRetentionGuardian
  class App
    DEFAULT_PORT = 4541

    def self.start
      port = Integer(ENV.fetch("PORT", DEFAULT_PORT.to_s))
      server = WEBrick::HTTPServer.new(
        Port: port,
        BindAddress: "127.0.0.1",
        AccessLog: [],
        Logger: WEBrick::Log.new($stderr, WEBrick::Log::WARN)
      )

      trap("INT") { server.shutdown }
      trap("TERM") { server.shutdown }

      mount_routes(server)

      puts "Message Retention Guardian running on http://127.0.0.1:#{port}"
      puts "Docs: http://127.0.0.1:#{port}/docs"
      server.start
    rescue Errno::EADDRINUSE
      warn "Message Retention Guardian could not start because port #{port} is already in use."
      warn 'Set a different port before running again, for example:'
      warn '$env:PORT = "4545"'
      warn 'ruby server.rb'
      exit 1
    end

    def self.mount_routes(server)
      server.mount_proc("/") do |_req, res|
        json(res, {
          service: "message-retention-guardian",
          status: "ok",
          docs: "/docs",
          dashboard: "/api/dashboard/summary"
        })
      end

      server.mount_proc("/docs") do |_req, res|
        json(res, {
          routes: [
            { method: "GET", path: "/" },
            { method: "GET", path: "/docs" },
            { method: "GET", path: "/api/dashboard/summary" },
            { method: "GET", path: "/api/sample" },
            { method: "GET", path: "/api/policies" },
            { method: "GET", path: "/api/requests/:id" },
            { method: "POST", path: "/api/analyze/request" }
          ]
        })
      end

      server.mount_proc("/api/dashboard/summary") do |_req, res|
        json(res, Analysis.summary)
      end

      server.mount_proc("/api/sample") do |_req, res|
        json(res, Analysis.sample_request)
      end

      server.mount_proc("/api/policies") do |_req, res|
        json(res, Analysis.policies)
      end

      server.mount_proc("/api/requests") do |req, res|
        request_id = req.path.split("/").last
        item = Analysis.find_request(request_id)
        if item
          json(res, item)
        else
          json(res, { error: "request not found" }, 404)
        end
      end

      server.mount_proc("/api/analyze/request") do |req, res|
        if req.request_method != "POST"
          json(res, { error: "method not allowed" }, 405)
          next
        end

        payload = req.body.to_s.empty? ? {} : JSON.parse(req.body)
        json(res, Analysis.evaluate(payload))
      rescue JSON::ParserError
        json(res, { error: "invalid json" }, 400)
      end
    end

    def self.json(res, payload, status = 200)
      res.status = status
      res["Content-Type"] = "application/json"
      res.body = JSON.pretty_generate(payload)
    end
  end
end

