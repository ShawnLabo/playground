package tube.shawn.java.demo;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.Getter;

class GetMessagesResponse {
    @Getter private List<Message> messages;

    public GetMessagesResponse(Iterable<Message> messages) {
        List<Message> messageList = new ArrayList<Message>();
        messages.forEach(messageList::add);
        this.messages = messageList;
    }
}

@RestController
@RequestMapping("/messages")
public class MessageController {

    @Autowired
    private MessageRepository messageRepository;

    @GetMapping("/")
    public GetMessagesResponse getMessages() {
        return new GetMessagesResponse(messageRepository.findAll());
    }

    @PostMapping("/")
    public Message createMessage(@RequestBody Message message) {
        messageRepository.save(message);
        return message;
    }
}
