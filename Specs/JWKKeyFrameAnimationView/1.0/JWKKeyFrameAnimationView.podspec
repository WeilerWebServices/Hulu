Pod::Spec.new do |s|
  s.name             =  'JWKKeyFrameAnimationView'
  s.version          =  '1.0'
  s.summary          =  'A view for displaying key-frame animations.'
  s.homepage         =  'https://github.com/jwkelso/JWKKeyFrameAnimationView'
  s.author           =  { 'James Kelso' => 'james.w.kelso@gmail.com' }
  s.source           =  { :git => 'https://github.com/jwkelso/JWKKeyFrameAnimationView.git', :tag => '1.0' }

  s.source_files     = 'JWKKeyFrameAnimationView/*.{h,m}'
  
  s.platform = :ios
  
  s.ios.frameworks   =  'QuartzCore'

  s.requires_arc     =  true

  s.prefix_header_contents = '#import "JWKKeyFrameAnimationView.h"'

  s.license  = { :type => 'MIT',
                 :text => 'JWKKeyFrameAnimationView (https://github.com/jwkelso/JWKKeyFrameAnimationView)

Copyright (c) 2013 James Kelso (http://www.jameskelso.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.' }

end
