#!/usr/bin/env ruby

require 'google_drive'
require 'fileutils'
require 'time'
require 'date'
require 'yaml'

require 'logger'
logger = Logger.new(STDOUT)
logger.level = Logger::WARN

config = {
  "google_client_id" => "google-id.json",
  "spreadsheets" => [
    "15I1o7Ch3lZYLE3b6vcQQYoxyLb-_x4HT_1r8ojwb6TM",
  ],
  "tab" => "2020-2021 Schedule",
}

cacheDir = "tea-times"



begin
  session = GoogleDrive::Session.from_config(config["google_client_id"])
  logger.info 'Generating data from Google spreadsheets...'
  spreadsheets = {}
  spreadsheets_updated = {}

  for sheetKey in config['spreadsheets']
    begin
      logger.warn "   from spreadsheet #{sheetKey}"
      spreadsheet = session.spreadsheet_by_key(sheetKey)

      for ws in spreadsheet.worksheets
        next if ws.title != config["tab"]
        
        begin
          list = []
          ws.list.each do |item|
            begin
              guest = item.to_hash
              next if guest['Name'].nil? or ['', '---'].include?(guest['Name'])

              t = Time.parse(guest['Date'])
              date = t.strftime("%Y-%m-%d")
              name =  guest['Name'].split().map(&:downcase).join('-')
              file = "#{cacheDir}/#{date}-#{name}.yml"
              puts file
              
              File.write file, item.to_hash.to_yaml
            rescue
              logger.warn "Issue with item: #{guest['Name']}"
            end
          end
        # rescue
        #   logger.warn "Error processing worksheet: #{$!}"
        end
      end
    # rescue
    #   logger.warn "Error processing spreadsheet: #{$!}"
    end
  end
# rescue
#   return logger.error "Failed to process Google spreadsheets: #{$!}"
end

  
