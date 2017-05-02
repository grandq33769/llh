package llh.selenium;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;

public class ChromeTest {

  private static ChromeDriverService service;
  private WebDriver driver;
  private StringBuffer verificationErrors = new StringBuffer();
  private static final String driverPath = "D:/Ecllipse/my-code/Java/selenium/chromedriver.exe";

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
    driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
  }

  @After
  public void quitDriver() {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

  @Test
  public void testGoogleSearch() throws InterruptedException {
    driver.get("http://www.google.com");
    //  Max the window
    driver.manage().window().maximize();

    // Locate the search input field by name = "q"
    WebElement element = driver.findElement(By.name("q"));

    // Text Input "Hello World" 
    element.sendKeys("Hello World");
            
    // simulate the click search button
    element.submit();

    // Check the title of the page
    System.out.println("Page title is: " + driver.getTitle());
    
    //Close the browser
    //sleep for 3 sec before close the browser
    Thread.sleep(3000);
  }
  
  @Test
  public void testSelenium() throws Exception {
    driver.get("http://www.fcu.edu.tw/wSite/mp?mp=1");
    driver.findElement(By.linkText("學術資源")).click();
    driver.findElement(By.cssSelector("div.np > ul > li > a[title=\"院系所-單位列表\"]")).click();
    driver.findElement(By.linkText("資訊工程學系")).click();
    driver.findElement(By.linkText("師資介紹")).click();
    driver.findElement(By.xpath("(//a[contains(text(),'系所師資')])[2]")).click();
    driver.findElement(By.xpath("(//button[@name='submit'])[55]")).click();
    try {
      assertEquals("陳錫民", driver.findElement(By.xpath("//div[@id='zone.content']/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr/td")).getText());
    } catch (Error e) {
      verificationErrors.append(e.toString());
    }
  }

  
  @Test
  public void testSeleniumTest6() throws Exception {
    driver.get("https://en.wikipedia.org/wiki/Main_Page");
    driver.findElement(By.id("searchInput")).clear();
    driver.findElement(By.id("searchInput")).sendKeys("Selenium ide");
    driver.findElement(By.id("searchButton")).click();
    try {
      assertEquals("Selenium", driver.findElement(By.cssSelector("p > b")).getText());
    } catch (Error e) {
      verificationErrors.append(e.toString());
    }
  }


}
