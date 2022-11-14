package tube.shawn.java.demo;

import lombok.Getter;

public class HelloMessage {

    @Getter private final String message;

    public HelloMessage(String message) {
        this.message = message;
    }

}
