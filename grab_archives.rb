# Archive API: 4d1f21d6ff81499887fc4250f23b75a6
# Article Search API: 4d1f21d6ff81499887fc4250f23b75a6

saveto="/home/mrware/Dropbox/Code/NYTimes API/JSON/test.json"

input=ARGV
month=ARGV[0]
year=ARGV[1]

require 'uri'
require 'net/http'
require 'json'
lookupRAW="https://api.nytimes.com/svc/archive/v1/YEAR/MONTH.json"
lookup=lookupRAW
lookup['MONTH']=month
lookup['YEAR']=year
saveto['test']=month+'-'+year
puts "Will save to ... "+saveto
puts "Looking up ... "+lookup

uri = URI(lookup)
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
uri.query = URI.encode_www_form({
  "api-key" => "4d1f21d6ff81499887fc4250f23b75a6"
})
request = Net::HTTP::Get.new(uri.request_uri)
@result = JSON.parse(http.request(request).body)

File.open(saveto,"w") do |f|
  # f.write(lookup)
  f.write(@result.to_json)
end
