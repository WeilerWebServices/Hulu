module Bwoken
  class Device
    class << self

      # deprecated. Remove when Rakefile support removed
      def should_use_simulator?
        want_simulator? || ! connected?
      end

      # deprecated. Remove when Rakefile support removed
      def want_simulator?
        ENV['SIMULATOR'] && ENV['SIMULATOR'].downcase == 'true'
      end

      def connected?
        self.uuid ? true : false
      end

      def uuid
        ioreg[/"USB Serial Number" = "([0-9a-z]+)"/] && $1
      end

      def device_type
        ioreg[/"USB Product Name" = "(.*)"/] && $1.downcase
      end

      def ioreg
        @ioreg ||= `ioreg -w 0 -rc IOUSBDevice -k SupportsIPhoneOS`
      end

    end

  end
end
