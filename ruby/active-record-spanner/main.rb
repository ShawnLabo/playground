# frozen_string_literal: true

require "active_record"


# Foreign key

class Product < ActiveRecord::Base
  has_many :orders
end

class Customer < ActiveRecord::Base
  has_many :orders
end

class Order < ActiveRecord::Base
  has_one :product
  has_one :customer
end


# Interleave

class Singer < ActiveRecord::Base
  has_many :albums
end

class Album < ActiveRecord::Base
  belongs_to :singer
  has_many :songs
end

class Song < ActiveRecord::Base
  belongs_to :album
end


ActiveRecord::Base.establish_connection(
  adapter: "spanner",
  project: ENV.fetch("GOOGLE_PROJECT_ID"),
  instance: ENV.fetch("SPANNER_INSTANCE"),
  database: ENV.fetch("SPANNER_DATABASE"),
)
