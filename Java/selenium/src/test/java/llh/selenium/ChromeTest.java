package llh.selenium;

import java.io.File;
import java.io.IOException;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;

public class ChromeTest {

  private static ChromeDriverService service;
  private WebDriver driver;
  private static final String driverPath = "C:/Users/LokHim/Desktop/Selenium/chromedriver.exe";

  @BeforeClass
  public static void createAndStartService() throws IOException {
    service = new ChromeDriverService.Builder().usingDriverExecutable(new File(driverPath))
        .usingAnyFreePort().build();
    service.start();
  }

  @AfterClass
  public static void createAndStopService() {
    service.stop();
  }

  @Before
  public void createDriver() {
    driver = new RemoteWebDriver(service.getUrl(), DesiredCapabilities.chrome());
  }

  @After
  public void quitDriver() {
    driver.quit();
  }

  @Test
  public void testGoogleSearch() throws InterruptedException {
    driver.get("http://www.google.com");
    //  Max the window
    driver.manage().window().maximize();

    // Locate the search input field by name = "q"
    WebElement element = driver.findElement(By.name("q"));

    // Text Input "Selenium" 
    element.sendKeys("Hello World");
            
    // simulate the click search button
    element.submit();

    // Check the title of the page
    System.out.println("Page title is: " + driver.getTitle());
    
    //Close the browser
    //sleep for 3 sec before close the browser
    Thread.sleep(3000);
  }
}
