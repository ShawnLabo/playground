package tube.shawn.java.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class HelloController {

    private static final String template = "Hellaao, %s!";

    @GetMapping("/hello")
    public HelloMessage hello(@RequestParam(value = "name", defaultValue = "World") String name) {
        return new HelloMessage(String.format(template, name));
    }

}
