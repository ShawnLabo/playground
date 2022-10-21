package tube.shawn.java.demo;

import java.util.UUID;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import org.hibernate.annotations.Type;

import lombok.Getter;


@Entity
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Type(type = "uuid-char")
    @Getter
    private UUID id;

    @Getter
    private String message;

    public Message(String message) {
        this.message = message;
    }

}
