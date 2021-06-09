#Use latest ruby
FROM ruby:latest

#Add copy of webiste
COPY docs /docs

#Install Jekyll
RUN gem install jekyll bundler

WORKDIR /docs

RUN bundle install

CMD ["bundle", "exec", "jekyll", "serve", "--livereload", "--host", "0.0.0.0"]

