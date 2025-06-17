FROM openjdk:22-jdk-slim

# Install wget, unzip, and curl
RUN apt-get update && apt-get install -y wget unzip curl

# Download and extract Tomcat 11
RUN curl -O https://dlcdn.apache.org/tomcat/tomcat-11/v11.0.7/bin/apache-tomcat-11.0.7.tar.gz \
    && tar xzf apache-tomcat-11.0.7.tar.gz \
    && mv apache-tomcat-11.0.7 /opt/tomcat \
    && rm apache-tomcat-11.0.7.tar.gz

# Remove default webapps
RUN rm -rf /opt/tomcat/webapps/*

# Copy your WAR file
COPY build/libs/OnlineBank.war /opt/tomcat/webapps/OnlineBank.war

# Expose port
EXPOSE 8080

# Start Tomcat
CMD ["/opt/tomcat/bin/catalina.sh", "run"] 