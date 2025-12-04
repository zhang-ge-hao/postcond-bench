https://github.com/sherlock-project/sherlock/blob/339634f7bc370517b06f960b464b10935bb829fb/./sherlock_project/sites.py#L213-L229
```
@icontract.snapshot(lambda self: dict(self.sites), name="old_sites")
@icontract.snapshot(lambda do_not_remove: [s.casefold() for s in do_not_remove], name="old_do_not_remove")
@icontract.ensure(
    lambda OLD, self: 
        isinstance(self.sites, dict)
        and
        all(((site in self.sites and self.sites[site] is OLD.old_sites[site]) if (not OLD.old_sites[site].is_nsfw or site.casefold() in OLD.old_do_not_remove) else (site not in self.sites)) for site in OLD.old_sites)
)
```
```
@icontract.snapshot(lambda self: dict(self.sites), name="old_sites")
@icontract.snapshot(lambda do_not_remove: [s.casefold() for s in do_not_remove], name="old_do_not_remove")
@icontract.ensure(lambda OLD, self: isinstance(self.sites, dict))
@icontract.ensure(lambda OLD, self: all(((site in self.sites and self.sites[site] is OLD.old_sites[site]) if (not OLD.old_sites[site].is_nsfw or site.casefold() in OLD.old_do_not_remove) else (site not in self.sites)) for site in OLD.old_sites))
```
[10]
===== 10 =====
```
             if self.sites[site].is_nsfw and site.casefold() not in do_not_remove:
                 continue
             sites[site] = self.sites[site]
-        self.sites =  sites+        self.sites =  None
```
```
    def remove_nsfw_sites(self, do_not_remove: list = []):
        """
        Remove NSFW sites from the sites, if isNSFW flag is true for site

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        None
        """
        sites = {}
        do_not_remove = [site.casefold() for site in do_not_remove]
        for site in self.sites:
            if self.sites[site].is_nsfw and site.casefold() not in do_not_remove:
                continue
            sites[site] = self.sites[site]
        self.sites =  None

```
